//go:build linux

package main

import (
	"bufio"
	"os"
	"os/exec"
	"regexp"
	"runtime"
	"strings"
	"sync"

	"github.com/sirupsen/logrus"
)

func RunLocalCore(domain, area string) (output []string) {
	var outputLock sync.Mutex
	var pool sync.WaitGroup
	dnsFileName := "./dns.txt"
	if _, err := os.Stat(dnsFileName); err != nil {
		panic("Can't find dns.txt")
	}
	file, err := os.Open(dnsFileName)
	if err != nil {
		panic("Can't open dns.txt")
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	logrus.Info("[+]Your system is ", runtime.GOOS)
	for scanner.Scan() {
		line := scanner.Text()
		pool.Add(1)
		go func(domain, line string) {
			var cmd *exec.Cmd
			var r *regexp.Regexp
			switch runtime.GOOS {
			case "windows":
				cmd = exec.Command("nslookup.exe", domain, line)
				r = regexp.MustCompile(`Addresses:\s+(\d+\.\d+\.\d+\.\d+)`)
			case "linux":
				cmd = exec.Command("nslookup", domain, line)
				r = regexp.MustCompile(`Address:\s+(\d+\.\d+\.\d+\.\d+)`)
			default:
				logrus.Error("[-]Unsupported system")
				return
			}
			if ip, err := cmd.CombinedOutput(); err == nil {
				tmpOutput := r.FindAllStringSubmatch(string(ip), -1)
				for _, tmpIP := range tmpOutput {
					if tmpIP[1] == line || strings.Contains(tmpIP[1], "#") {
						logrus.Debug("[-]ignore", tmpIP[0], " -> ", tmpIP[1])
						continue
					}
					logrus.Debug(tmpIP[0], " -> ", tmpIP[1])
					outputLock.Lock()
					output = append(output, tmpIP[1])
					outputLock.Unlock()
				}
			}
			pool.Done()
		}(domain, line)
	}
	pool.Wait()
	return output
}
