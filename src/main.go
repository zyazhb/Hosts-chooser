package main

import (
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/sirupsen/logrus"
)

type config struct {
	os        int
	hostsPath string
}

var Config config

func main() {
	Init()
	res := []HostsItem{}
	reslock := sync.RWMutex{}
	var domain string

	if os.Getenv("DEBUG") == "1" {
		logrus.SetLevel(logrus.DebugLevel)
		logrus.Debug("Debug on")
	}
	if os.Args[1] != "" {
		domain = os.Args[1]
	} else {
		fmt.Scanln(&domain)
	}
	logrus.Infof("[+]Testing domain %s...", domain)
	iplist := RunRemoteCore(domain, "asia")
	wg := sync.WaitGroup{}
	logrus.Info("[+]Testing delay...")
	for _, ip := range iplist {
		ip0 := ip
		wg.Add(1)
		go func() {
			delay := Delay(domain, ip0)
			logrus.Infof("[+]Delay: %s - %s", ip0, delay)
			if delay != time.Duration(-1) {
				reslock.Lock()
				res = append(res, HostsItem{HostsName: domain, Ip: ip0, Delay: int(delay)})
				reslock.Unlock()
			}
			wg.Done()
		}()
	}
	wg.Wait()
	if len(res) == 0 {
		logrus.Error("[-]No result")
		return
	}
	logrus.Infof("[+]Results: %v", res)
	logrus.Infof("[+]Trying add hosts to file: %s", Config.hostsPath)
	HItemsToSystemHosts(res)
	logrus.Infof("[+]Add to hosts file done!")
}
