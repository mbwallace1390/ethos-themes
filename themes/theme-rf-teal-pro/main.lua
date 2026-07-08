-- RF Teal Pro
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
        key = "RFTeal",
        name = "RF Teal Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x13, 0x2F, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xC8, 0xC0), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x09, 0x1D, 0x1D), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x05, 0x11, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0x00, 0xC8, 0xC0), -- ACTIVE_COLOR
            lcd.RGB(0x65, 0x96, 0x93), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0xC8, 0xC0), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x26, 0x54, 0x52), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x05, 0x11, 0x11), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-rf-teal-pro.png", "toolbar-rf-teal-pro-x18.png")),
    })
end

return {
    init = init
}
