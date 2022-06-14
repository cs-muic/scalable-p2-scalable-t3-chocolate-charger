import "./Widget.scss"
import List from "./List"
import axios from "axios";
import { Button } from "@mui/material";

const Widget = () => {

    var temp2;

    function sentRequest(){
        axios.post("http://127.0.0.1:5000/api/doing_bucket",
        {
            "bucket":"name"
        }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    return (
        <div className="widget">
            <div className="widgetName">Videos</div>
                <div className="bigButton">
                    <Button onClick={sentRequest()}>Hello</Button>
                </div>
                <div className="videos">
                    <List/>
                </div>
        </div>
    )
}

export default Widget