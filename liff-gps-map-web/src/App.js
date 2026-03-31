import React, { useEffect, useState } from "react";
import liff from "@line/liff";
import "./App.css";
import { GoogleMap, LoadScript, MarkerF } from "@react-google-maps/api";
import { ClipLoader } from "react-spinners";
import { parseLambdaBody } from "./lib/api";

const EMPTY_MARKER = { lat: null, lng: null };

function validLatLng(m) {
  if (!m || m.lat == null || m.lng == null) return false;
  const lat = Number(m.lat);
  const lng = Number(m.lng);
  return Number.isFinite(lat) && Number.isFinite(lng);
}

function App() {
  const [message, setMessage] = useState("");
  const [markers, setMarkers] = useState([
    { ...EMPTY_MARKER },
    { ...EMPTY_MARKER },
    { ...EMPTY_MARKER },
  ]);
  const [timestamps, setTimestamps] = useState(["", "", ""]);
  const [isLoading, setIsLoading] = useState(true);

  const containerStyle = {
    height: "100%",
    width: "100%",
  };

  const center = {
    lat: 35.69575,
    lng: 139.77521,
  };

  useEffect(() => {
    liff.init({ liffId: process.env.REACT_APP_LIFF_ID }).then(() => {
      const line_accesstoken = liff.getAccessToken();
      const body = JSON.stringify({ access_token: line_accesstoken });

      const get_gps_data = (payload) => {
        fetch(process.env.REACT_APP_MAP_API, {
          method: "POST",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
          body: payload,
        })
          .then((response) => response.json())
          .then((res) => {
            const parsed = parseLambdaBody(res);
            const data_res = typeof parsed === "string" ? JSON.parse(parsed) : parsed;

            try {
              const row = data_res.Data[0];
              const nextMarkers = [
                { ...EMPTY_MARKER },
                { ...EMPTY_MARKER },
                { ...EMPTY_MARKER },
              ];
              const nextTs = ["", "", ""];
              for (let i = 1; i <= 3; i++) {
                try {
                  const pos = row[`No${i}`].gnss;
                  const pos_time = row[`No${i}`].time_stamp;
                  const [latStr, lngStr] = pos.split(",");
                  nextMarkers[i - 1] = {
                    lat: parseFloat(latStr, 10),
                    lng: parseFloat(lngStr, 10),
                  };
                  nextTs[i - 1] = pos_time;
                } catch (e) {
                  console.error(e);
                }
              }
              setMarkers(nextMarkers);
              setTimestamps(nextTs);
              setMessage("正常に動作しています。");
              setIsLoading(false);
            } catch (e) {
              console.error(e);
              setMessage("データがありません。");
              setIsLoading(false);
            }
          })
          .catch((err) => console.error(err));
      };
      get_gps_data(body);
    });
  }, []);

  const mapCenter = validLatLng(markers[0])
    ? { lat: Number(markers[0].lat), lng: Number(markers[0].lng) }
    : center;

  return (
    <div className="App">
      {isLoading ? (
        <div className="App-sippner">
          <ClipLoader loading={isLoading} />
        </div>
      ) : (
        <>
          <div className="App-map">
            <div className="App-map-inner">
              <LoadScript
                googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAP_KEY}
              >
                <GoogleMap
                  mapContainerStyle={containerStyle}
                  center={mapCenter}
                  zoom={17}
                >
                  {validLatLng(markers[0]) ? (
                    <MarkerF
                      position={{
                        lat: Number(markers[0].lat),
                        lng: Number(markers[0].lng),
                      }}
                      label={"1"}
                    />
                  ) : null}
                  {validLatLng(markers[1]) ? (
                    <MarkerF
                      position={{
                        lat: Number(markers[1].lat),
                        lng: Number(markers[1].lng),
                      }}
                      label={"2"}
                    />
                  ) : null}
                  {validLatLng(markers[2]) ? (
                    <MarkerF
                      position={{
                        lat: Number(markers[2].lat),
                        lng: Number(markers[2].lng),
                      }}
                      label={"3"}
                    />
                  ) : null}
                </GoogleMap>
              </LoadScript>
            </div>
          </div>
          <div className="App-record">
            <div className="App-numbers">
              <p className="App-number">
                <span>1</span> : {timestamps[0]}
              </p>
              <p className="App-number">
                <span>2</span> : {timestamps[1]}
              </p>
              <p className="App-number">
                <span>3</span> : {timestamps[2]}
              </p>
            </div>
          </div>
          <p className="App-status">{message}</p>
          <button
            type="button"
            className="App-btn"
            onClick={() => window.location.reload()}
          >
            ReLoad
          </button>
        </>
      )}
    </div>
  );
}

export default App;
