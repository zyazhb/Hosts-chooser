//go:build linux

package main

import (
	"bufio"
	"os"
	"os/exec"
	"regexp"
	"sync"
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
	for scanner.Scan() {
		line := scanner.Text()
		go func(domain, line string) {
			pool.Add(1)
			cmd := exec.Command("nslookup", domain, line)
			if ip, err := cmd.CombinedOutput(); err == nil {
				r := regexp.MustCompile(`Address: (\d.*)`)
				tmpOutput := r.FindAllStringSubmatch(string(ip), -1)
				for _, tmpIP := range tmpOutput {
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
