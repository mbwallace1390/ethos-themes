-- OLED Red
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
        key = "OLRed",
        name = "OLED Red",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x16, 0x0F, 0x10), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x48, 0x4E, 0x56), -- DISABLE_COLOR
            lcd.RGB(0x0B, 0x08, 0x08), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xA2, 0xAD), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- ACTIVE_COLOR
            lcd.RGB(0x64, 0x63, 0x64), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3B, 0x4F), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3A, 0x38, 0x38), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-oled-red.png", "toolbar-oled-red-x18.png")),
    })
end

return { init = init }
