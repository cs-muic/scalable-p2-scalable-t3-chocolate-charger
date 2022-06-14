import React, { useState, useEffect } from "react";
import axios from 'axios'
import ListBox from 'react-listbox';


const List = () => {
    const [vidnames, setVidnames] = useState([]);
    var temp2;
    
    const getNames = () =>  { 
        axios.post("http://127.0.0.1:5000/api/list_objs",
            {
                "bucket":"video"
            }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            console.log(typeof(temp2))
            setVidnames(temp2);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getNames(), [])
    
    function sentRequest(name){
        axios.post("http://127.0.0.1:5000/api/make_gif",
        {
            "filename": name
        }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            console.log("res", res.data);
            console.log(`sent ${name}`);
          })
          .catch(err => {
            console.log("error in request", err);
          });

        console.log(name);
    }

    
    return (
            <ul>
                {vidnames.map((vid) => <h1 onClick={() => sentRequest(vid)}>{vid}</h1>)}
            </ul>
    )
}

export default List