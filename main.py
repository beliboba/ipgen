import asyncio
import aiofiles
from ipaddress import ip_address


async def get_ranges():
	async with aiofiles.open('ranges.txt', 'r') as f:
		lines = await f.readlines()
		return list(map(lambda x: x.split(','), lines))


async def out(iplist: list):
	async with aiofiles.open('out.txt', 'a+') as f:
		for ipaddr in iplist:
			if f"{ipaddr}\n" not in await f.readlines():
				await f.write(f'{ipaddr}\n')


async def main():
	for lines in await get_ranges():
		for line in lines:
			startip = int(ip_address(line.split('-')[0].strip()).packed.hex(), 16)
			endip = int(ip_address(line.split('-')[1].strip()).packed.hex(), 16)
			for ip in range(int(ip_address(startip)), int(ip_address(endip))):
				iplist = [ip_address(ip).exploded for ip in range(startip, endip)]
				await out(iplist)


if __name__ == '__main__':
	asyncio.run(main())
