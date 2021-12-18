package main

import (
	"testing"
)

func TestHItemsToSystemHosts(t *testing.T) {
	hostsItem := HostsItem{"test", "127.0.0.1", 0}
	hostsItems := []HostsItem{hostsItem}
	Config.hostsPath = "/tmp/hosts"
	HItemsToSystemHosts(hostsItems)
}
