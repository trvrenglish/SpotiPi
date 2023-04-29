package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strconv"
	"strings"
	"sync"
)

const (
	osascript string  = "/usr/bin/osascript"
	minNoise  float32 = 135000
	maxNoise  float32 = 110000
)

type NoiseReading struct {
	Noise   int     `json:"noise_level"`
	Voltage float32 `json:"voltage"`
}

func main() {
	readings := make(chan int)
	waitGroup := sync.WaitGroup{}
	for {
		waitGroup.Add(2)
		go func() {
			defer waitGroup.Done()
			getPiVolumeAt1SecInterval(readings)
		}()

		go func() {
			defer waitGroup.Done()
			setSystemVolume(readings)
		}()
		waitGroup.Wait()
	}
}

// this will run in a go function with no end continuously feeding averages to the readings chan
func getPiVolumeAt1SecInterval(readings chan<- int) {
	// make http GET request that receives the last 10 readings
	// make the requests asynchronous
	noiseReading := &NoiseReading{}
	client := &http.Client{}
	doGetRequest(noiseReading, client)
	readings <- noiseReading.Noise
}

func doGetRequest(noiseReading *NoiseReading, client *http.Client) int {
	req, _ := http.NewRequest("GET", "http://10.90.134.107:5000", nil)
	data, _ := client.Do(req)
	json.NewDecoder(data.Body).Decode(noiseReading)
	return noiseReading.Noise
}

// if this runs in an infinite loop
func setSystemVolume(readings <-chan int) {
	// based on the value in the reading from the channel
	// the range could be a number between 133000 and 110000 noise level
	// normalize it over a certain range
	vol := normalize(<-readings)
	setVolume(vol)
}

func normalize(noiseLevel int) int {
	rangeNoise := maxNoise - minNoise
	return int((1 - ((float32(noiseLevel) - minNoise) / rangeNoise)) * 100)
}

func setVolume(vol int) {
	if vol > 100 || vol < 0 {
		return
	}
	setVol := fmt.Sprintf("set volume output volume %d", vol)
	cmd := exec.Command(osascript, "-e", setVol)
	cmd.Run()
}

func getVolume() int {
	cmd := exec.Command(osascript, "-e", "get volume settings")
	outBytes, err := cmd.Output()
	if err != nil {
		panic(fmt.Errorf("calling osascript command: %w", err))
	}
	vol, _ := strconv.Atoi(strings.Split(strings.Split(string(outBytes), ",")[0], ":")[1])
	return vol
}
