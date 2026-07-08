-- Carbon
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
        key = "Carbon",
        name = "Carbon",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x22, 0x27, 0x2D), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xB7, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x64, 0x67, 0x6C), -- DISABLE_COLOR
            lcd.RGB(0x16, 0x1A, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x84, 0xDA, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0C, 0x0E, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x00, 0xB7, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x76, 0x79, 0x7D), -- INACTIVE_COLOR
            lcd.RGB(0x18, 0xBD, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x47, 0x4B, 0x4F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0C, 0x0E, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-carbon.png", "toolbar-carbon-x18.png")),
    })
end

return { init = init }
