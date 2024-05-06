import asyncio
import asyncua


PORT = 4840
URI = 'http://examples.freeopcua.github.io'
OBJ = 'OBJ'


async def main():
    svr = asyncua.Server()
    await svr.init()
    svr.set_endpoint(f'opc.tcp://0.0.0.0:{PORT}')

    idx = await svr.register_namespace(URI)
    obj = await svr.nodes.objects.add_object(idx, OBJ)
    var1 = await obj.add_variable(idx, 'value_float', 0.0)
    var2 = await obj.add_variable(idx, 'value_int', 0)
    var3 = await obj.add_variable(idx, 'value_string', '')
    await var1.set_writable()
    await var2.set_writable()
    await var3.set_writable()

    async with svr:
        while True:
            await asyncio.sleep(0.1)


asyncio.run(main())
