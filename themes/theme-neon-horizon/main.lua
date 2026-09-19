-- Neon Horizon
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-neon-horizon.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "NeoHor",
        name = "Neon Horizon",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF7, 0xF1, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x2B, 0x1B, 0x49), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x4F, 0xB8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x25, 0x0A, 0x20), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x80, 0x6A, 0x92), -- DISABLE_COLOR
            lcd.RGB(0x1A, 0x12, 0x30), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD9, 0xBA, 0xF4), -- SECONDARY_COLOR
            lcd.RGB(0x5F, 0xE8, 0xA5), -- SAFE_COLOR
            lcd.RGB(0x0B, 0x07, 0x16), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4D, 0x6D), -- ERROR_COLOR
            lcd.RGB(0x34, 0xD8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x98, 0x82, 0xAA), -- INACTIVE_COLOR
            lcd.RGB(0x34, 0xD8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x58, 0x36, 0x6F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD1, 0x66), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x11), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0B, 0x07, 0x16), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-neon-horizon.png", "toolbar-neon-horizon-x18.png"),
    })
end

return { init = init }
