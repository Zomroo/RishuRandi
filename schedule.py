import asyncio


async def schedule_waifu(client, chat_id, waifu_name, time_in_minutes):
    await asyncio.sleep(time_in_minutes * 1)
    waifu_message = f"Who will catch {waifu_name}? /catch {waifu_name}"
    await client.send_message(chat_id, waifu_message)
