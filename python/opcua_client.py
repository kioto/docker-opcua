import asyncio
from asyncua import Client


PORT = 4840
URL = f'opc.tcp://localhost:{PORT}'
URI = 'http://examples.freeopcua.github.io'
OBJ = 'OBJ'


async def read(vname, var):
    val = await var.read_value()
    if isinstance(val, str):
        print(f'READ: {vname} = "{val}"')
    else:
        print(f'READ: {vname} = {val}')


async def write(vname, var, val):
    await var.write_value(val)
    if isinstance(val, str):
        print(f'WRITE: {vname} = "{val}"')
    else:
        print(f'WRITE: {vname} = {val}')


async def main():
    async with Client(url=URL) as client:
        idx = await client.get_namespace_index(URI)
        var_float = await client.nodes.root.get_child(['0:Objects',
                                                       f'{idx}:{OBJ}',
                                                       f'{idx}:value_float'])
        var_int = await client.nodes.root.get_child(['0:Objects',
                                                     f'{idx}:{OBJ}',
                                                     f'{idx}:value_int'])
        var_str = await client.nodes.root.get_child(['0:Objects',
                                                     f'{idx}:{OBJ}',
                                                     f'{idx}:value_string'])

        await read('var_float', var_float)
        await read('var_int', var_int)
        await read('var_str', var_str)
        print()

        await write('var_float', var_float, 1.1)
        await write('var_int', var_int, 123)
        await write('var_str', var_str, 'Hello')
        print()

        await read('var_float', var_float)
        await read('var_int', var_int)
        await read('var_str', var_str)
        print()

        await write('var_float', var_float, 2.2)
        await write('var_int', var_int, 456)
        await write('var_str', var_str, 'World')
        print()

        await read('var_float', var_float)
        await read('var_int', var_int)
        await read('var_str', var_str)


if __name__ == '__main__':
    asyncio.run(main())
