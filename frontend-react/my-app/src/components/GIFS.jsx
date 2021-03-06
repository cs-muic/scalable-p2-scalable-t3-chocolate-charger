import React, { useEffect, useState } from "react";
import axios from 'axios';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';

const GIFS = () => {

    const [urls, setUrls] = useState([]);
    var temp2;
    
    const getNames = () =>  { 
        axios.get("http://127.0.0.1/api/get_urls"
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            setUrls(temp2);
            console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }


    useEffect(() => getNames(), [])

    //const [buckets, setBuckets] = useState([]);
    
    //console.log(buckets)
    return (
        // <img 
        // src="http://localhost:9000/gif/1.gif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minio%2F20220613%2F%2Fs3%2Faws4_request&X-Amz-Date=20220613T171542Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=f5e0d38e6e0f3b146197f5e6658410b8c825c482f139e37e93f205f0f95916ae"
        // alt="new"
        // />
        // <ul>
        //     {urls.map((url) => <img src={`data:image/jpeg;base64,${url}`} alt="new"/>)}
        // </ul>

        <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
        {urls.map((url) => (
            <ImageListItem key={url}>
            <img
                src={`data:image/jpeg;base64,${url}`}
                //srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
                loading="lazy"
            />
            </ImageListItem>
        ))}
        </ImageList>

    )

    
}

export default GIFS