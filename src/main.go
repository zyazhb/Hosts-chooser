package main

import (
	"os"
	"sync"
	"time"

	"github.com/sirupsen/logrus"
)

func main() {
	res := make(map[string]time.Duration)
	reslock := sync.RWMutex{}
	domain := os.Args[1]
	logrus.Infof("[+]Testing domain %s...", domain)
	iplist := run_remote_core(domain, "asia")
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
	logrus.Infof("[+]Results:", res)
}
