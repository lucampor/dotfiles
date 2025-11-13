return {
  'nvim-orgmode/orgmode',
  event = 'VeryLazy',
  ft = { 'org' },
  config = function()
    -- Setup orgmode
    require('orgmode').setup {
      org_agenda_files = '~/org/journal.org',
      org_default_notes_file = '~/org/notes.org',
      org_todo_keywords = { 'TODO(t)', 'WAIT(t)', '[ ](k)', '[-]', '[#]', '[?]', '[!]', '|', '[V](v)', '[X](x)', 'DONE(d)', 'CANCELLED(c)' },
      org_startup_folded = 'showeverything',
      org_ellipsis = ' ⮷',
      org_hide_leading_stars = true,
      org_todo_keyword_faces = {
        ['TODO'] = ':foreground "maroon" :weight bold',
        ['DONE'] = ':foreground "#1E90FF" :weight bold',
        ['CANCELED'] = ':foreground "#FF3030" :weight bold',
        ['WAIT'] = ':foreground "#FDFF1F" :weight bold',
      },
    }

    -- NOTE: If you are using nvim-treesitter with ~ensure_installed = "all"~ option
    -- add ~org~ to ignore_install
    -- require('nvim-treesitter.configs').setup({
    --   ensure_installed = 'all',
    --   ignore_install = { 'org' },
    -- })
  end,
}
