-- OLED Green
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
        key = "OLGrn",
        name = "OLED Green",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x0F, 0x16, 0x11), -- SECONDARY_BGCOLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- HIGHLIGHT_COLOR
            lcd.RGB(0x08, 0x0B, 0x09), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x48, 0x4E, 0x56), -- DISABLE_COLOR
            lcd.RGB(0x08, 0x0B, 0x09), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xA2, 0xFB, 0xC0), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- ACTIVE_COLOR
            lcd.RGB(0x62, 0x65, 0x65), -- INACTIVE_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x37, 0x3A, 0x39), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-oled-green.png", "toolbar-oled-green-x18.png")),
    })
end

return { init = init }
