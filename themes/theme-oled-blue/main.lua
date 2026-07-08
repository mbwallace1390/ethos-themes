-- OLED Blue
-- Lightweight standalone ETHOS theme.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "OLBlue",
        name = "OLED Blue",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x0F, 0x12, 0x16), -- SECONDARY_BGCOLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x48, 0x4E, 0x56), -- DISABLE_COLOR
            lcd.RGB(0x08, 0x09, 0x0B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9C, 0xC7, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x62, 0x63, 0x66), -- INACTIVE_COLOR
            lcd.RGB(0x2F, 0x8C, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x37, 0x39, 0x3B), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-oled-blue.png", "toolbar-oled-blue-x18.png")),
    })
end

return { init = init }
