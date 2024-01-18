linux:
	CGO_ENABLED=0 go build -ldflags="-s -w" .
windows:
	CGO_ENABLED=0  GOOS=windows go build -ldflags="-s -w" -o Host-chooser.exe *.go
all: linux windows
