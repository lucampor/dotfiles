return {
  {
    "nvim-telescope/telescope-file-browser.nvim",
    dependencies = { "nvim-telescope/telescope.nvim", "nvim-lua/plenary.nvim" },
    extensions = {
      file_browser = {
        theme = "ivy",
        -- disables netrw and use telescope-file-browser in its place
        hijack_netrw = true,
        mappings = {
          ["i"] = {
            -- your custom insert mode mappings
          },
          ["n"] = {
            -- your custom normal mode mappings
          },
        },
      },
    },
    config = function()
     vim.keymap.set("n", "<space>.", ":Telescope file_browser<CR>")
     -- open file_browser with the path of the current buffer
     vim.keymap.set("n", "<space>fp", ":Telescope file_browser path=%:p:h select_buffer=true<CR>")
    end,
  }
}
