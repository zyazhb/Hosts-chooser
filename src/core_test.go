package main

import (
	"sync"
	"testing"
)

func TestCore(t *testing.T) {
	run_remote_core("github.com", "china")
}

func TestDelay(t *testing.T) {
	iplist := []string{
		"52.78.231.108", "164.124.101.2", "164.124.101.2", "52.78.231.108", "164.124.101.2", "164.124.101.2", "13.234.210.38", "175.101.80.33", "175.101.80.33", "13.234.210.38", "175.101.80.33", "175.101.80.33"}
	wg := sync.WaitGroup{}
	for _, ip := range iplist {
		ip0 := ip
		wg.Add(1)
		go func() {
			delay := Delay("github.com", ip0)
			t.Log(delay)
			wg.Done()
		}()
	}
	wg.Wait()
}
