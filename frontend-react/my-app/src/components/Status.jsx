import React, { useState, useEffect } from "react";
import axios from 'axios'

const Status = () => {
    const [status, setStatus] = useState([]);
    var temp3;
    
    const getStatus = () =>  { 
        axios.get("http://127.0.0.1/api/get_status"
        ).then(res => {
            console.log(res);
            temp3 = res.data;
            console.log(temp3)
            setStatus(temp3);
            // console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getStatus(), [])
    
    return (
            <ul>
                {status.map((sta) => <h1>{sta}</h1>)}
            </ul>
    )
}

export default Status