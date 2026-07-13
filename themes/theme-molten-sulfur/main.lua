-- Molten Sulfur
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
        key = "MltSulf",
        name = "Molten Sulfur",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF1, 0xEC), -- PRIMARY_COLOR
            lcd.RGB(0x21, 0x1B, 0x17), -- SECONDARY_BGCOLOR
            lcd.RGB(0xCF, 0xFF, 0x3D), -- HIGHLIGHT_COLOR
            lcd.RGB(0x10, 0x0C, 0x0A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x63, 0x5F, 0x5C), -- DISABLE_COLOR
            lcd.RGB(0x15, 0x11, 0x0F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xE4, 0xF7, 0x9D), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0A, 0x08, 0x07), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xF4, 0xA3), -- ACTIVE_COLOR
            lcd.RGB(0x73, 0x6F, 0x6C), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xF4, 0xAC), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x46, 0x42, 0x40), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0A, 0x08, 0x07), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-molten-sulfur.png", "toolbar-molten-sulfur-x18.png")),
    })
end

return { init = init }
