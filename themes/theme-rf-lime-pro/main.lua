-- RF Lime Pro
-- Lightweight RF Pro outline-focus color variant.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "RFLime",
        name = "RF Lime Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x2A, 0x34, 0x13), -- SECONDARY_BGCOLOR
            lcd.RGB(0xA8, 0xF0, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x17, 0x21, 0x08), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x17, 0x21, 0x08), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x0D, 0x13, 0x04), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xA8, 0xF0, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0x8E, 0xA5, 0x64), -- INACTIVE_COLOR
            lcd.RGB(0xA8, 0xF0, 0x00), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4C, 0x5E, 0x22), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0D, 0x13, 0x04), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-rf-lime-pro.png", "toolbar-rf-lime-pro-x18.png")),
    })
end

return {
    init = init
}
