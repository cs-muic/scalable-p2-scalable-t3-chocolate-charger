import React from "react";
import List from './List'
import Sidebar from "./Sidebar";
import WidgetVideo from "./widgetVideo";
import WidgetStatus from "./widgetStatus";
import './home.scss'


const Home = () => { 
    return (
        <div className="home">
            <Sidebar/>
            <div className="homeContainer">
                <div className="widgets">
                    <WidgetVideo/>
                    <WidgetStatus/>
                </div>
            </div>
        </div>
    )
}

export default Home