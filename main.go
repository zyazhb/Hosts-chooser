package main

import (
	"flag"
	"sync"
	"time"

	"strings"

	"github.com/sirupsen/logrus"
)

func main() {
	domain := flag.String("d", "", "domain")
	debug := flag.Bool("debug", false, "debug")
	autoInsert := flag.Bool("auto", false, "auto insert fastest IP to /etc/hosts")
	flag.Parse()
	if *domain == "" {
		logrus.Error("[-]Please specify a domain")
		flag.Usage()
		return
	}
	if *debug {
		logrus.SetLevel(logrus.DebugLevel)
		logrus.Debug("[+]Debug mode")
	}
	res := make(map[string]time.Duration)
	reslock := sync.RWMutex{}
	logrus.Infof("[+]Testing domain %s...", *domain)
	iplist := RunLocalCore(*domain, "")
	wg := sync.WaitGroup{}
	logrus.Info("[+]Testing delay...")
	for _, ip := range iplist {
		ip0 := ip
		wg.Add(1)
		go func() {
			delay := Delay(*domain, ip0)
			logrus.Infof("[+]Delay: %s - %s", ip0, delay)
			if delay != time.Duration(-1) {
				reslock.Lock()
				res[ip0] = delay
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
	logrus.Info("[+]Results:", res)

	var fastestIP string
	var fastestDelay time.Duration = time.Duration(1<<63 - 1)

	logrus.Debug("[+]Finding fastest IP...")
	for ip, delay := range res {
		logrus.Debugf("  %s: %s", ip, delay)
		if delay < fastestDelay {
			fastestDelay = delay
			fastestIP = ip
			logrus.Debugf("  -> New fastest: %s (%s)", ip, delay)
		}
	}

	if fastestIP != "" {
		logrus.Infof("[+]Fastest IP by delay: %s (%s)", fastestIP, fastestDelay)

		if *autoInsert {
			if err := updateHostsFile(*domain, fastestIP); err != nil {
				// Check if it's an OS compatibility issue
				if strings.Contains(err.Error(), "not implemented for") {
					logrus.Info("[-]Skipping hosts file update due to OS compatibility")
				} else {
					logrus.Error("[-]Failed to update /etc/hosts: ", err)
				}
			}
		} else {
			logrus.Infof("[+]To auto-update /etc/hosts, use --auto flag")
		}
	} else {
		logrus.Warn("[-]No fastest IP found")
	}
}
