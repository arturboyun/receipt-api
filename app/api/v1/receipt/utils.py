from app.api.v1.receipt.models import Receipt


class ReceiptPrinter:
    @staticmethod
    def print_receipt(receipt: Receipt, width: int = 80):
        name_width = 50
        price_width = width - name_width - 5

        receipt_lines = [
            f"{receipt.user.name}".center(width),
        ]

        for product in receipt.products:
            price = "{:,.2f}".format(product.price).rjust(price_width)
            receipt_lines.append(f"{product.quantity:,.2f} x {price}")
            if len(product.name) > width - len(product.name):
                receipt_lines.append(f"{product.name[:width - 3]}...")
                receipt_lines.append(f"{product.total:>{width},.2f}")
            else:
                receipt_lines.append(f"{product.name}{product.total:>{width - len(product.name):},.2f}")

            receipt_lines.append("-" * width)

        payment_type_text = "Картка" if receipt.payment.type == "card" else "Готівка"

        total_line = f"СУМА{receipt.total:>{width - len('СУМА'):},.2f}"
        receipt_lines.append(total_line)
        receipt_lines.append(f"{payment_type_text}{receipt.total:>{width - len(payment_type_text):},.2f}")
        receipt_lines.append(f"Решта{receipt.rest:>{width - len('Решта'):},.2f}")

        receipt_lines.append("=" * width)

        datetime_line = f"{receipt.payment.created_at.strftime('%d.%m.%Y %H:%M')}"
        receipt_lines.append(datetime_line.center(width))
        receipt_lines.append("Дякуємо за покупку!".center(width))

        for line in receipt_lines:
            yield line + "\n"
