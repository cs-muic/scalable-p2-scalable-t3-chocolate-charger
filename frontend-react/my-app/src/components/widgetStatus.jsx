import "./Widget.scss"
import Status from "./Status"

const WidgetStatus = () => {
    return (
        <div className="widget">
            <div className="widgetName">Status</div>
                <div className="status">
                    <Status/>
                </div>
        </div>
    )
}

export default WidgetStatus
