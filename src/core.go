package main

import (
	"bufio"
	"embed"
	"io/ioutil"
	"net/http"
	"os/exec"
	"regexp"
	"strings"
	"time"

	"github.com/sirupsen/logrus"
)

func RunRemoteCore(domain, area string) (output []string) {
	logrus.Info("[+]Finding ips remote core...")
	resp, err := http.Get("https://en.ipip.net/dns.php?a=dig&host=" + domain + "&area%5B%5D=" + area)
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

//go:embed dns.txt
var dnsfile embed.FS
var cache = make(map[string]bool)

func RunLocalCore(domain string) (output []string) {
	f, err := dnsfile.Open("dns.txt")
	if err != nil {
		logrus.Error(err)
	}
	r := bufio.NewReader(f)
	tmp, _ := r.ReadString(' ')
	dns := strings.Split(string(tmp), "\n")
	for _, v := range dns {
		switch Config.os {
		case Windows:
			_ = exec.Command("dig", domain, v, "+short")
		case Linux:
			tmp := Nslookup(domain, v)
			if _, ok := cache[tmp]; !ok {
				cache[tmp] = true
				output = append(output, string(tmp))
			}
		default:
			logrus.Error("Unknown Platform")
		}
	}
	return
}

func Nslookup(args ...string) string {
	cmd := exec.Command("nslookup", args[0], args[1])
	stdout, _ := cmd.StdoutPipe()
	if err := cmd.Start(); err != nil {
		logrus.Error("Execute failed when Start:" + err.Error())
	}
	out_bytes, _ := ioutil.ReadAll(stdout)
	stdout.Close()
	if err := cmd.Wait(); err != nil {
		logrus.Error("Execute failed when Wait:" + err.Error())
	}
	tmp := regexp.MustCompile(`Address:\s*(.*)`).FindAllSubmatch(out_bytes, 2)[1][1]
	return string(tmp)
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
