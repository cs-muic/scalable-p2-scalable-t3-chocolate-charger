import React, { useState, useEffect } from "react";
import axios from 'axios'


const Status = () => {
    const [status, setStatus] = useState([]);

    var temp2;

    function sentRequest(jobId){
        axios.post("http://127.0.0.1/api/status",
        {
            "jobId": {jobId}
        }
    ).then(res => {
        console.log(res);
        temp2 = res.data;
        setStatus(temp2);
        // console.log("res", res.data);
      })
      .catch(err => {
        console.log("error in request", err);
      });
    }


    return (
        <div>
            <ul onClick={() => sentRequest(1)}>1</ul>
        </div>
    )
}

export default Status