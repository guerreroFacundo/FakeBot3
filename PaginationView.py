import discord


class PaginationView(discord.ui.View):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.current_page = 1
        self.sep = 1  # Esto debería ser 1 si cada página es un único embed
        self.message = None

    async def update_message(self):
        self.update_buttons()
        if self.message:
            try:
                current_data = self.get_current_page_data()
                # await discord.Interaction.edit_original_response(embed=current_data, view=self)
                await self.message.edit(embed=current_data, view=self)
            except discord.HTTPException as e:
                print(f"Failed to edit message: {e}")

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False

        if self.current_page == int(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False

    def get_current_page_data(self):
        # Dado que sep = 1, solo deberías obtener un único embed
        index = self.current_page - 1  # Los índices de la lista empiezan en 0
        return self.data[index]

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message()

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.current_page > 1:
            self.current_page -= 1
            await self.update_message()

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.current_page < int(len(self.data) / self.sep):
            self.current_page += 1
            await self.update_message()

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep)
        await self.update_message()

