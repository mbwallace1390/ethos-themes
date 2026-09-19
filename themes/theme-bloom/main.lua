-- Bloom
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

local function init()
    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
    -- Load the optional palette-matched logo once; failures keep the theme usable.
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-bloom.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Bloom",
        name = "Bloom",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x33, 0x2B, 0x44), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x6F, 0xB5), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7A, 0x75, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x1E, 0x14, 0x30), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF9, 0xB9, 0xDB), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x0C, 0x08, 0x12), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xA9, 0x8C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x97, 0x94, 0xA1), -- INACTIVE_COLOR
            lcd.RGB(0xB0, 0x97, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4D, 0x46, 0x5C), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0C, 0x08, 0x12), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-bloom.png", "toolbar-bloom-x18.png"),
    })
end

return { init = init }
