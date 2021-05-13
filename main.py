import tzevaadom


def handler(List_Alerts):
    for alert in List_Alerts:
        message = "New Alarm: " + alert["name_en"] + ". Zone: " + alert["zone_en"]
        print(message)


''' start monitor api '''
tzevaadom.alerts_listener(handler)  # listening to alerts in background (Thread)