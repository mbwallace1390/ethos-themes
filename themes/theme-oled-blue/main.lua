-- OLED Blue
-- Lightweight standalone ETHOS theme.
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
    system.registerTheme({
        key = "OLBlue",
        name = "OLED Blue",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x0F, 0x12, 0x16), -- SECONDARY_BGCOLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x26, 0x27, 0x27), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5C, 0x61, 0x68), -- DISABLE_COLOR
            lcd.RGB(0x08, 0x09, 0x0B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9C, 0xC7, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x7C, 0x7C, 0x7F), -- INACTIVE_COLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x37, 0x39, 0x3B), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-oled-blue.png", "toolbar-oled-blue-x18.png"),
    })
end

return { init = init }
