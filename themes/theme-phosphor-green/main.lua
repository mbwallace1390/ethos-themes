-- Phosphor Green
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
        key = "PhosGr",
        name = "Phosphor Green",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xB8, 0xFA, 0xBB), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x2E, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0x54, 0xFF, 0x54), -- HIGHLIGHT_COLOR
            lcd.RGB(0x09, 0x14, 0x09), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5E, 0x68, 0x60), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x1F, 0x10), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xA8, 0xFB, 0xAA), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x08, 0x11, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x54, 0xFF, 0x54), -- ACTIVE_COLOR
            lcd.RGB(0x6C, 0x75, 0x6E), -- INACTIVE_COLOR
            lcd.RGB(0x54, 0xFF, 0x54), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x45, 0x51, 0x46), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x11, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-phosphor-green.png", "toolbar-phosphor-green-x18.png")),
    })
end

return { init = init }
