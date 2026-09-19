-- Midnight Blueprint
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-midnight-blueprint.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "MidBpt",
        name = "Midnight Blueprint",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xE7, 0xF6, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x14, 0x36, 0x51), -- SECONDARY_BGCOLOR
            lcd.RGB(0x62, 0xC8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x07, 0x18, 0x26), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x87, 0x9B), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x26, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xB5, 0xE1, 0xF8), -- SECONDARY_COLOR
            lcd.RGB(0x58, 0xE6, 0x9A), -- SAFE_COLOR
            lcd.RGB(0x07, 0x17, 0x25), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5B, 0x68), -- ERROR_COLOR
            lcd.RGB(0xF4, 0xF7, 0xFA), -- ACTIVE_COLOR
            lcd.RGB(0x81, 0x9F, 0xB3), -- INACTIVE_COLOR
            lcd.RGB(0xF4, 0xF7, 0xFA), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x34, 0x5C, 0x77), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x6A), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x07, 0x17, 0x25), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-midnight-blueprint.png", "toolbar-midnight-blueprint-x18.png"),
    })
end

return { init = init }
