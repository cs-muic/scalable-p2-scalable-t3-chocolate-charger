import React, { useEffect, useState } from "react";

const GIFS = () => {

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
            setVidnames(temp2);
            // console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getNames(), [])




    //const [buckets, setBuckets] = useState([]);
    
    //console.log(buckets)
    return (
        <img 
        src="http://localhost:9000/gif/1.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minio%2F20220613%2F%2Fs3%2Faws4_request&X-Amz-Date=20220613T171542Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=f5e0d38e6e0f3b146197f5e6658410b8c825c482f139e37e93f205f0f95916ae"
        alt="new"
        />
        <ul>
                {vidnames.map((vid) => <img src=>{vid}</h1>)}
        </ul>
    )

    
}

export default GIFS