package main

import (
	"bufio"
	"context"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/schollz/progressbar/v3"
	"github.com/sirupsen/logrus"
)

func RunLocalCore(domain, area string) (output []string) {
	execPath, _ := os.Executable()
	dnsFile := filepath.Join(filepath.Dir(execPath), "dns.txt")

	dnsServers := readDNSServers(dnsFile)
	logrus.Info("[+]Your system is ", runtime.GOOS)
	logrus.Info("[+]Processing ", len(dnsServers), " DNS servers...")

	bar := progressbar.Default(int64(len(dnsServers)), "DNS lookups")
	results := make(chan string, len(dnsServers))
	var wg sync.WaitGroup

	for _, server := range dnsServers {
		wg.Add(1)
		go func(server string) {
			defer wg.Done()
			defer bar.Add(1)

			if ip := lookupDNS(domain, server); ip != "" {
				results <- ip
			}
		}(server)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	for ip := range results {
		output = append(output, ip)
	}

	bar.Finish()
	logrus.Info("[+]DNS lookup completed! Found ", len(output), " results")
	return output
}

func readDNSServers(filename string) []string {
	file, err := os.Open(filename)
	if err != nil {
		panic("Can't find dns.txt: " + err.Error())
	}
	defer file.Close()

	var servers []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		if line := strings.TrimSpace(scanner.Text()); line != "" {
			servers = append(servers, line)
		}
	}
	return servers
}

func lookupDNS(domain, server string) string {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	var cmd *exec.Cmd
	var pattern string

	if runtime.GOOS == "windows" {
		cmd = exec.CommandContext(ctx, "nslookup.exe", domain, server)
		pattern = `Addresse?s?:\s+(\d+\.\d+\.\d+\.\d+)`
	} else {
		cmd = exec.CommandContext(ctx, "nslookup", domain, server)
		pattern = `Address:\s+(\d+\.\d+\.\d+\.\d+)`
	}

	output, err := cmd.CombinedOutput()
	if err != nil {
		return ""
	}

	re := regexp.MustCompile(pattern)
	matches := re.FindAllStringSubmatch(string(output), -1)

	for _, match := range matches {
		ip := match[1]
		if ip != server && !strings.Contains(ip, "#") {
			return ip
		}
	}
	return ""
}
