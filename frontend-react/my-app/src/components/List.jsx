import React, { useState, useEffect } from "react";
import axios from 'axios'
import { ListItemButton } from "@mui/material";


const List = () => {
    const [vidnames, setVidnames] = useState([]);
    var temp2;
    
    const getNames = () =>  { 
        axios.post("http://127.0.0.1/api/list_objs",
            {
                "bucket":"video"
            }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            setVidnames(temp2);
            // console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getNames(), [])
    
    function sentRequest(name){
        axios.post("http://127.0.0.1/api/make_gif",
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
        // <div id='listbox-control'>
        //     <h4>Select your favorite car:</h4>
        //     <ListBox>
        //         {vidnames.map((vid) => <li>{vid}</li>)}
        //     </ListBox>
        // </div>
            <ul>
                {vidnames.map((vid) => <ListItemButton
                className='button'
                onClick={() => sentRequest(vid)}>{vid}</ListItemButton>)}
            </ul>
    )
}

export default List