package main

import (
	"fmt"
	"os"
	"runtime"
	"strings"

	"github.com/sirupsen/logrus"
)

func updateHostsFile(domain, ip string) error {
	// Check if running on Linux
	if runtime.GOOS != "linux" {
		logrus.Warn("[-]Hosts file update is only implemented for Linux systems")
		logrus.Infof("[+]Current OS: %s - Hosts file update skipped", runtime.GOOS)
		return fmt.Errorf("hosts file update not implemented for %s", runtime.GOOS)
	}

	hostsFile := "/etc/hosts"
	comment := fmt.Sprintf("# Added by hosts-chooser for %s", domain)
	newEntry := fmt.Sprintf("%s\t%s\t%s", ip, domain, comment)

	content, err := os.ReadFile(hostsFile)
	if err != nil {
		return fmt.Errorf("failed to read %s: %v", hostsFile, err)
	}

	lines := strings.Split(string(content), "\n")
	var newLines []string
	replaced := false

	commentPattern := fmt.Sprintf("# Added by hosts-chooser for %s", domain)

	for _, line := range lines {
		if strings.Contains(line, commentPattern) {
			newLines = append(newLines, newEntry)
			replaced = true
			logrus.Info("[+]Replaced existing entry for ", domain)
		} else if !replaced && strings.Fields(line) != nil && len(strings.Fields(line)) >= 2 {
			fields := strings.Fields(line)
			if len(fields) >= 2 && fields[1] == domain && !strings.Contains(line, "hosts-chooser") {
				logrus.Debug("[-]Skipping existing entry for ", domain, ": ", line)
				continue
			}
			newLines = append(newLines, line)
		} else {
			newLines = append(newLines, line)
		}
	}

	if !replaced {
		newLines = append(newLines, newEntry)
		logrus.Info("[+]Added new entry for ", domain)
	}

	newContent := strings.Join(newLines, "\n")
	if err := os.WriteFile(hostsFile, []byte(newContent), 0644); err != nil {
		return fmt.Errorf("failed to write %s: %v", hostsFile, err)
	}

	logrus.Info("[+]Successfully updated ", hostsFile, " with ", domain, " -> ", ip)
	return nil
}
