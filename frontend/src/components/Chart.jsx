import React, { useEffect, useRef, useState } from "react";
// import {Chartjs} from "chart.js";
import Chartjs from "chart.js/auto";

const API_ENDPOINT= process.env.REACT_APP_API_ENDPOINT;


const chartConfig = {
  type: "bar",
  data: {
    labels: [],
    datasets: [
      {
        label: "新規感染者数       ---  [表示]ボタンをクリックしてください  ---",
        fill: true,
        lineTension: 0.1,
        backgroundColor: "rgba(75,192,192,0.4)",
        borderColor: "rgba(75,192,192,1)",
        borderCapStyle: "round",
        borderDash: [],
        hoverRadius: 5,
        hoverBackgroundColor: "rgba(75,192,192,1)",
        hoverBorderColor: "rgba(220,220,220,1)",
        hoverBorderWidth: 1,
        borderRadius: 1,
        data: [],
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  },
};

export const Chart = (props) => {
  const chartContainer = useRef(null);
  const [chartInstance, setChartInstance] = useState(null);

  const [message, setMessage] = useState("");
  const { todate } = props;
  const { fromdate } = props;

  useEffect(() => {
    // if (chartContainer && chartContainer.current) {
    if (chartInstance === null) {
      const newChartInstance = new Chartjs(chartContainer.current, chartConfig);
      setChartInstance(newChartInstance);
    }
  }, [chartContainer, chartInstance]);

  const updateDataset = (datasetIndex, newData, newLabel) => {
    chartInstance.data.datasets[datasetIndex].data = newData;
    chartInstance.data.datasets[datasetIndex].label = "新規感染者数";
    chartInstance.data.labels = newLabel;
    chartInstance.update();
  };

  const onClickShow = () => {
    const requestOptions = {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ todate: todate, fromdate: fromdate }),
    };
    
    fetch(API_ENDPOINT + "/getdata", requestOptions)
      .then((res) => {
        return res.json();
      })
      .then((json) => {
        if (json.status === "ERROR") {
          setMessage(json.message);
          return;
        }

        updateDataset(0, json.message.data, json.message.labels);
        setMessage("");
      })
      .catch((error) => {
        setMessage("Error for accesing to " + API_ENDPOINT + "/getdata");
        return;
    })
    ;
  };

  return (
    <div>
      <div className="message-area">
        {message.length > 0 ? (
          <div className="alert alert-dismissible alert-danger">
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="alert"
              onClick={() => setMessage("")}
            ></button>
            {message}
          </div>
        ) : null}
      </div>
      <div className="col-sm-2">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => onClickShow()}
        >
          表示
        </button>
      </div>
       <canvas ref={chartContainer} /> 
    </div>
  );
};
