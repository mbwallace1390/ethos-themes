-- Desert Tactical
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "DesTac",
        name = "Desert Tactical",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0x2E, 0x24, 0x18), -- PRIMARY_COLOR
            lcd.RGB(0xC9, 0xB3, 0x8C), -- SECONDARY_BGCOLOR
            lcd.RGB(0xA8, 0x5C, 0x24), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xF8, 0xEA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x8C, 0x7C, 0x64), -- DISABLE_COLOR
            lcd.RGB(0xE3, 0xD2, 0xB1), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x62, 0x4A, 0x32), -- SECONDARY_COLOR
            lcd.RGB(0x3B, 0x84, 0x58), -- SAFE_COLOR
            lcd.RGB(0xF1, 0xE7, 0xD2), -- PAGE_BGCOLOR
            lcd.RGB(0xB8, 0x38, 0x32), -- ERROR_COLOR
            lcd.RGB(0x7B, 0x3E, 0x17), -- ACTIVE_COLOR
            lcd.RGB(0x96, 0x7E, 0x5F), -- INACTIVE_COLOR
            lcd.RGB(0x7B, 0x3E, 0x17), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB2, 0x9B, 0x74), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA1, 0x5E, 0x00), -- WARNING_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xF1, 0xE7, 0xD2), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-desert-tactical.png", "toolbar-desert-tactical-x18.png")),
    })
end

return { init = init }
