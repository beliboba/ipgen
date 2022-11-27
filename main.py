from ipaddress import ip_address
import asyncio
import aiofiles


async def get_ranges():
	async with aiofiles.open('ranges.txt', 'r') as f:
		lines = await f.readlines()
		return list(map(lambda x: x.split(','), lines))


async def out(iplist: list):
	cleanlist = list(dict.fromkeys(iplist))
	for ipaddr in cleanlist:
		async with aiofiles.open('out.txt', 'a+') as f:
			if f"{ipaddr}\n" not in await f.readlines():
				await f.write(f'{ipaddr}\n')


async def main():
	ips = []
	for lines in await get_ranges():
		for line in lines:
			startip = int(ip_address(line.split('-')[0].strip()).packed.hex(), 16)
			endip = int(ip_address(line.split('-')[1].strip()).packed.hex(), 16)
			iplist = [ip_address(ip).exploded for ip in range(startip, endip)]
			ips.extend(iplist)
	await out(ips)


if __name__ == '__main__':
	asyncio.run(main())
