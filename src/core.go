package main

import (
	"io/ioutil"
	"net/http"
	"regexp"
	"strings"
	"time"

	"github.com/sirupsen/logrus"
)

func run_remote_core(domain, area string) (output []string) {
	logrus.Info("[+]Finding ips remote core...")
	resp, err := http.Get("http://en.ipip.net/dns.php?a=dig&host=" + domain + "&area%5B%5D=" + area)
	if err != nil {
		logrus.Error(err)
		return
	}
	defer resp.Body.Close() //在回复后必须关闭回复的主体
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logrus.Error(err)
		return
	}
	r := regexp.MustCompile(`\d+\.\d+\.\d+\.\d+`)
	iplist := r.FindAll(body, -1)
	logrus.Infof("[+]Got domain! \n%s ", iplist)
	for _, ip := range iplist {
		output = append(output, string(ip[:]))
	}
	return output
}

func Delay(domain, ip string) time.Duration {
	starttime := time.Now()
	Client := &http.Client{Timeout: time.Duration(5 * time.Second)}
	req, err := http.NewRequest("GET", "https://"+ip+"/", nil)
	if err != nil {
		logrus.Error(err)
		return time.Duration(-1)
	}
	req.Host = domain
	resp, err := Client.Do(req)
	if strings.Contains(err.Error(), "x509: cannot validate certificate ") {
		return time.Since(starttime)
	} else if err != nil {
		logrus.Error(err)
		return time.Duration(-1)
	}
	defer resp.Body.Close()
	return time.Since(starttime)
}
