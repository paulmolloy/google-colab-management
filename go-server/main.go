package main

import ("fmt"
"log"
"net/http"
"os"
"path"
"encoding/json"
"io/ioutil"

"github.com/gorilla/mux"
)

const ssl_dir = "/etc/letsencrypt/live/paulmolloy.me"
const cert_name = "fullchain.pem"
const private_key_name = "privkey.pem"
const port = "8443"


type ngrokTunnel struct { 
    ID string `json:"Token"`
    User string `json:"User"`
    URL string `json:"URL"`
    Port string `json:"Port"`
    RawURL string  `json:"RawURL"`
}

var ngrokTunnels map[string]ngrokTunnel


func indexHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Let's see if this works, CI included! Fabric working!")
}

func indexHandler_clear_text(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "SLL connection didn't worked so this is clear text!")
}

func setTunnelHandler(w http.ResponseWriter, r *http.Request) {

    var newTunnel ngrokTunnel
	reqBody, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Fprintf(w, "Kindly enter data with the event title and description only in order to update")
	}
	
	json.Unmarshal(reqBody, &newTunnel)
	ngrokTunnels[newTunnel.ID] = newTunnel
	w.WriteHeader(http.StatusCreated)

	json.NewEncoder(w).Encode(newTunnel)
}

func getOneTunnelHandler(w http.ResponseWriter, r *http.Request) {
	ngrokTunnelID := mux.Vars(r)["id"]
	ngrokTunnel := ngrokTunnels[ngrokTunnelID]
	if ngrokTunnelID == "" {
			fmt.Fprintf(w, "A tunnel for ID not found.")
		}
		

	json.NewEncoder(w).Encode(ngrokTunnel)
}


func main() {
	cert_path := path.Join(ssl_dir, cert_name)
	key_path := path.Join(ssl_dir, private_key_name)

    ngrokTunnels = make(map[string]ngrokTunnel)

    ngrokTunnels["test"] =  ngrokTunnel{ 
        ID: "test",
        User: "root",
        URL: "0.tcp.ngrok.io",
        Port: "16942",
        RawURL: "root@tcp://0.tcp.ngrok.io:16988",
    }

	srv := NewServer(port)
	if _, err := os.Stat(cert_path); err != nil {
		log.Printf("%s does not exist: starting http server instead.", cert_path)
		srv.ListenAndServe()
	}else if _, err := os.Stat(key_path); err != nil {
		log.Printf("%s does not exist: starting http server instead.", key_path)
		srv.ListenAndServe()
	}else { // Else not very idiomatic.
		err := srv.ListenAndServeTLS(cert_path, key_path)
		if(err != nil) {
			log.Fatal(err)
		}
	}
}


func NewServer(port string) *http.Server {
	// Extra comment delete.
	addr := fmt.Sprintf(":%s", port)
	r := mux.NewRouter()
	
	
	r.HandleFunc("/", indexHandler)
    r.HandleFunc("/google-colab-manager/api/tunnel", setTunnelHandler).Methods("POST")
    r.HandleFunc("/google-colab-manager/api/tunnels/{id}", getOneTunnelHandler).Methods("GET")

	return &http.Server{
		Addr: addr,
		Handler: r,
	}
}
