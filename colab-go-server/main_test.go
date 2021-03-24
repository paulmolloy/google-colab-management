package main

import ("bytes"
"crypto/tls"
"net/http"
"testing"
"io/ioutil"
"path"
"time"
)

func TestStartSSLServer(t *testing.T) {
	// Looked at this:
	// https://blog.dnsimple.com/2017/08/how-to-test-golang-https-services/
	certFile := "test_cert.pem"
	keyFile := "test_key.pem"
	ssl_dir := ""
        cert_path := path.Join(ssl_dir, certFile)
        key_path := path.Join(ssl_dir, keyFile)
	httpsPort := "8000"

	srv := NewServer(httpsPort)
	go srv.ListenAndServeTLS(cert_path, key_path)
	defer srv.Close()

	time.Sleep(100* time.Millisecond)

	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	client := &http.Client{Transport: tr}
	url := urlFor("https", httpsPort, "/")
	res, err := client.Get(url)

	if err != nil {
		t.Fatal(err)
	}

	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		t.Errorf("Response code was %v; want 200", res.StatusCode)
	}

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		t.Fatal(err)
	}

	expected := []byte("Let's see if this works, CI included! Fabric working!")

	if bytes.Compare(expected, body) != 0 {
		t.Errorf("Response body was '%v'; want '%v;'", expected, body)
	}
}

func urlFor(scheme string, serverPort string, path string) string {
	return scheme + "://localhost:" + serverPort + path
}
