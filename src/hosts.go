package main

import (
	"bufio"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"runtime"

	"github.com/sirupsen/logrus"
)

type hostsItem struct {
	HostsName string
	Ip        string
}

func HItemsToSystemHosts(hosts []hostsItem) {
	for _, h := range hosts {
		r := regexp.MustCompile(h.HostsName)
		f, err := os.Open(Config.hostsPath)
		if err != nil {
			logrus.Error(err)
		}
		fileScanner := bufio.NewScanner(f)
		hosts := ""
		for fileScanner.Scan() {
			if r.FindAllString(fileScanner.Text(), -1) != nil {
				hosts += h.HostsName + " " + h.Ip + "\n"
			} else {
				hosts += fileScanner.Text() + "\n"
			}
		}
		if err := ioutil.WriteFile(Config.hostsPath, []byte(h.HostsName+"    "+h.Ip), os.ModePerm); err != nil {
			logrus.Error(err)
		}
	}
}

func Init() {
	Config.hostsPath = "/etc/hosts"
	if runtime.GOOS == "windows" {
		Config.hostsPath = getWinSystemDir()
		Config.hostsPath = filepath.Join(Config.hostsPath, "system32", "drivers", "etc", "hosts")
	}
}

func getWinSystemDir() string {
	dir := ""
	if runtime.GOOS == "windows" {
		dir = os.Getenv("windir")
	}

	return dir
}
