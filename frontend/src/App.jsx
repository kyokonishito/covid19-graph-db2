import "./App.css";
import "bootswatch/dist/cerulean/bootstrap.min.css";
import { useState } from "react";
import { Chart } from "./components/Chart";

export const App = () => {
  const [toDate, setToDate] = useState(new Date().toISOString().split("T")[0]);
  const [fromDate, setFromDate] = useState("2020-02-13");
  

  return (
    <>
      <h1>COVID-19 東京新規感染者数</h1>
      <div className="input-area">
        <div className="form-group row">
          <label htmlFor="fromDate" className="col-sm-1 col-form-label">
            From Date
          </label>
          <div className="col-sm-4">
            <input
              id="fromDate"
              type="date"
              className="form-control"
              value={fromDate}
              onChange={(e) => setFromDate( e.target.value)}
            />
          </div>
          <label htmlFor="toDate" className="col-sm-1 col-form-label">
            To Date
          </label>
          <div className="col-sm-4">
            <input
              id="toDate"
              type="date"
              className="form-control col-sm-4"
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
            />
          </div>
        </div>
      </div>
      
      <div className="graph-area">
        
        <Chart fromdate={fromDate} todate={toDate} />
      </div>
    </>
  );
};
