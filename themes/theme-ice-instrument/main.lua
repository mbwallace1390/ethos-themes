-- Ice Instrument
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
        key = "IceIns",
        name = "Ice Instrument",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xCE, 0xF2, 0xFC), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x2A, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x8E, 0xEB, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0B, 0x13, 0x14), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5F, 0x66, 0x69), -- DISABLE_COLOR
            lcd.RGB(0x11, 0x1C, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC4, 0xF1, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x09, 0x0F, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x8E, 0xEB, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x6C, 0x74, 0x77), -- INACTIVE_COLOR
            lcd.RGB(0x8E, 0xEB, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x45, 0x4E, 0x51), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x09, 0x0F, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-ice-instrument.png", "toolbar-ice-instrument-x18.png")),
    })
end

return { init = init }
