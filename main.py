from PIL import Image
from io import BytesIO
import aiohttp
import asyncio

async def _sess():
    return aiohttp.ClientSession()
    
async def run():
    session = await _sess()
    async with session.get('https://raw.githubusercontent.com/ow0x/owo-cogs/main/pokebase/data/template.webp') as response:
        baseimg = await response.read()
    baseimg = BytesIO(baseimg)

    for id in range(1,916):
        
        base_image = Image.open(baseimg).convert("RGBA")
        #base_image.save('output/base_img.png')
        bg_width, bg_height = base_image.size
        id = str(id)
        if len(id) == 1:
            id = '00'+id
        elif len(id) == 2:
            id = '0'+id
        bg_width, bg_height = base_image.size
        base_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{id}.png"
        
        try:
            async with session.get(base_url) as response:
                if response.status != 200:
                    print(f'Error in {id}')
                    continue
                data = await response.read()
        except asyncio.TimeoutError:
            print(f"Error in {id}")

        pbytes = BytesIO(data)
        poke_image = Image.open(pbytes)
        poke_width, poke_height = poke_image.size
        poke_image_resized = poke_image.resize((int(poke_width * 1.6), int(poke_height * 1.6)))

        # if False:
        #     p_load = poke_image_resized.load()
        #     for y in range(poke_image_resized.size[1]):
        #         for x in range(poke_image_resized.size[0]):
        #             if p_load[x, y] == (0, 0, 0, 0):  # type: ignore
        #                 continue
        #             else:
        #                 p_load[x, y] = (1, 1, 1)  # type: ignore
        
        paste_w = int((bg_width - poke_width) / 10)
        paste_h = int((bg_height - poke_height) / 4)
        base_image.paste(poke_image_resized, (paste_w, paste_h), poke_image_resized)

        temp = BytesIO()
        
        base_image.save(f'images/revealed/{id}.png')
        
        temp.seek(0)
        
        pbytes.close()
        base_image.close()
        poke_image.close()
        print(f'Done {id}')
        
        
asyncio.run(run())
print('Done')