-- Ember Signal
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
        key = "EmbSig",
        name = "Ember Signal",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x2E, 0x25, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x8A, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x14, 0x0F, 0x09), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x64, 0x60), -- DISABLE_COLOR
            lcd.RGB(0x1F, 0x18, 0x10), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xC3, 0x82), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x11, 0x0D, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3B, 0x30), -- ACTIVE_COLOR
            lcd.RGB(0x75, 0x71, 0x6E), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3B, 0x30), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x4B, 0x46), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x0D, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-ember-signal.png", "toolbar-ember-signal-x18.png")),
    })
end

return { init = init }
