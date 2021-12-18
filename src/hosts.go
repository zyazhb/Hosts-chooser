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

type HostsItem struct {
	HostsName string
	Ip        string
	Delay     int
}

func HItemsToSystemHosts(hosts []HostsItem) {
	f, err := os.Open(Config.hostsPath)
	if err != nil {
		logrus.Error(err)
	}
	fileScanner := bufio.NewScanner(f)
	origin := []byte{}
	for fileScanner.Scan() {
		origin = append(origin, fileScanner.Bytes()...)
		origin = append(origin, []byte("\n")...)
	}
	for _, h := range hosts {
		r := regexp.MustCompile(`^` + `(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}\s+` + h.HostsName)
		origin = r.ReplaceAll(origin, []byte(h.Ip+" "+h.HostsName+"#Hosts_chooser"))
		logrus.Debug("origin is", origin)
	}

	if err := ioutil.WriteFile(Config.hostsPath, []byte(origin), os.ModePerm); err != nil {
		logrus.Error(err)
	}
}

const (
	Windows = iota
	Linux
)

func Init() {
	Config.os = Windows
	Config.hostsPath = "/etc/hosts"
	if runtime.GOOS == "windows" {
		Config.os = Linux
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
