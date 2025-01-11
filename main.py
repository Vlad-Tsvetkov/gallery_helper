from connections import client, app, slack_event_adapter
from funcs import extract_links, recovery_check


@slack_event_adapter.on('app_mention')
def mention(payload: dict):
    event = payload.get('event', {})
    thread_id = event.get('ts')
    channel_id = event.get('channel')
    mention_text = event.get('text')
    links = extract_links(text=mention_text)
    if links:
        result = recovery_check(links)
        formatted_result = "\n\n".join(
            f":white_check_mark: `можно восстановить` `{link}`" if status == "YES" else
            ":x: потрачено" if status == "NO" else
            f":warning: Укажи почту аккаунта, нет информации по `{link}`"
            for status, link in result
        )

        all_no = all(status == "NO" for status, _ in result)
        if all_no:
            client.reactions_add(
                channel=channel_id,
                timestamp=thread_id,
                name="x"
            )
        else:
            client.chat_postMessage(channel=channel_id, thread_ts=thread_id, text=formatted_result)
    else:
        client.chat_postMessage(channel=channel_id, thread_ts=thread_id, text="Не понимаю, о чём ты")


if __name__ == "__main__":
    app.run()
